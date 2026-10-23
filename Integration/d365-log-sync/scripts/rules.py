# -*- coding: utf-8 -*-
"""D365 日志同步 - 异常场景判定（动态读配置表）+ 报错字段拼接

设计原则：异常场景判定**每次执行实时读取多维表格「异常场景判定配置」表**，
配置表更新后立即生效，不依赖本地静态规则。本地静态规则（judge_abnormal_fallback）
仅在配置表拉取失败/为空时作为兜底。
"""


def judge_abnormal(scenario, response, config_rules=None):
    """依据「异常场景判定配置」表动态判定异常场景。

    Args:
        scenario: 集成场景名称（如 "Push WO to SCM"）
        response: Response JSON 文本
        config_rules: 配置表拉取的规则列表，每项为 dict:
            {'scenario': 场景, 'keyword': 关键词, 'abnormal': 异常场景}
            （已按配置表顺序排列；为 None/空时回退到本地静态规则）

    Returns:
        (异常场景, 是否命中配置, 是否兜底)
    """
    # 特殊优先级：Push WO to SCM + 无 errorCodeDesc → Maitrox-接口问题-其他（须发告警卡片）
    if _has_no_error_code_desc(scenario, response):
        return "Maitrox-接口问题-其他", False, False

    # 优先用配置表规则动态判定
    if config_rules:
        resp_lower = (response or "").lower()

        # 第一轮：匹配有具体关键词的规则
        for rule in config_rules:
            scen = (rule.get('scenario') or '').strip()
            kw = (rule.get('keyword') or '').strip()
            ab = (rule.get('abnormal') or '').strip()
            if not scen or not kw or not ab:
                continue
            if scen == scenario and kw.lower() in resp_lower:
                return ab, True, False

        # 第二轮：关键词匹配失败，查找该场景的空关键词兜底规则
        for rule in config_rules:
            scen = (rule.get('scenario') or '').strip()
            kw = (rule.get('keyword') or '').strip()
            ab = (rule.get('abnormal') or '').strip()
            if scen == scenario and not kw and ab:
                # 命中兜底规则（关键词为空 = 默认赋值）
                return ab, False, True

        # 配置表中该场景无任何规则（包括空关键词） -> 按场景兜底
        return _fallback(scenario), False, True

    # 配置表不可用 -> 回退到本地静态规则
    return judge_abnormal_fallback(scenario, response)


def _has_no_error_code_desc(scenario, response):
    """判断是否为「Push WO to SCM + Response 中无 errorCodeDesc」。
    此场景的「报错」列为空，但仍需触发告警（备件申请列表保留）。
    优先级高于配置表规则，因为「缺少字段」无法用关键词 in 匹配。
    """
    if scenario != "Push WO to SCM":
        return False
    if not response or not response.strip():
        return False
    import json as _json
    try:
        obj = _json.loads(response)
        if isinstance(obj, dict):
            data = obj.get("data") or obj
        elif isinstance(obj, list):
            data = obj[0] if obj else {}
        else:
            return True  # 非 JSON 结构，视为无 errorCodeDesc
    except Exception:
        return True  # 解析失败，视为无 errorCodeDesc
    if isinstance(data, dict):
        err = data.get("errorCodeDesc")
        return not err or (isinstance(err, str) and not err.strip())
    return True


def _fallback(scenario):
    """配置表未命中时的兜底：
    迈创 -> Maitrox-接口问题-其他（不新增配置表）；
    其他场景 -> 待补充（自动新增配置表）。
    """
    if scenario == "Push WO to SCM":
        return "Maitrox-接口问题-其他"
    return "待补充"


def judge_abnormal_fallback(scenario, response):
    """本地静态规则（仅在配置表拉取失败/为空时使用）。
    返回: (异常场景, 是否命中配置, 是否兜底)
    """
    if scenario == "Push WO to SCM":
        # 无 errorCodeDesc → Maitrox-接口问题-其他（须发告警）
        if _has_no_error_code_desc(scenario, response):
            return "Maitrox-接口问题-其他", False, False
        if "BOM" in response or "ERR_000090" in response:
            return "Maitrox-数据问题-out of SBOM", True, False
        if "Product SKU" in response:
            return "Maitrox-数据问题-主数据缺失", True, False
        return "Maitrox-接口问题-其他", False, True

    if scenario == "B2X Update WO Request":
        if "Cannot skip" in response or " is empty" in response:
            return "B2X-接口问题-必填为空", True, False
        if "status cannot move back" in response or "is Cancelled" in response or "is Closed" in response:
            return "B2X-接口问题-数据", True, False
        if "open Send-In order" in response:
            return "B2X-接口问题-工单重复", True, False
        return "待补充", False, False

    if scenario == "B2X Create WO Request":
        if "is empty" in response:
            return "B2X-接口问题-必填为空", True, False
        if "Existing active SWAP/Refund" in response:
            return "B2X-接口问题-工单重复", True, False
        return "待补充", False, False

    if scenario in ("MySav Update WO Request", "MySav Create WO Request"):
        if " is empty" in response or "[WoClosedDateTime] invalid format" in response:
            return "MySav-接口问题-必填为空", True, False
        if "Cannot skip" in response:
            return "MySav-接口问题-状态", True, False
        return "待补充", False, False

    return "待补充", False, False


def extract_keyword(response):
    """从 Response JSON 提取代表性关键词，用于配置表自动新增时识别该组合。
    优先级：data.errorCodeDesc（截断）> data.errorCode > 整体 JSON（截断）。
    返回字符串；无法提取时返回空。
    """
    if not response:
        return ""
    import json as _json
    try:
        obj = _json.loads(response)
        if isinstance(obj, dict):
            data = obj.get("data") or obj
        elif isinstance(obj, list):
            data = obj[0] if obj else {}
        else:
            data = None
    except Exception:
        data = None

    def pick(keys):
        if not isinstance(data, dict):
            return ""
        for k in keys:
            v = data.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, (int, float)):
                return str(v)
        return ""

    desc = pick(["errorCodeDesc", "errorDesc", "errorCode", "code", "message", "msg"])
    if desc:
        return desc[:40]

    try:
        s = _json.dumps(obj, ensure_ascii=False)
    except Exception:
        s = str(response)
    return s[:40]


def build_error_text(scenario, response):
    """构造「报错」字段值。
    Maitrox-数据问题-out of SBOM：取 data.errorCodeDesc，若 data.otherDesc 非空则拼接
      errorCodeDesc + "\\n超BOM物料: " + otherDesc(逗号转", ")
    其他场景：仅取 errorCodeDesc（response 为纯文本时，返回空）
    """
    import json as _json
    data = None
    if response and response.strip().startswith(("{", "[")):
        try:
            obj = _json.loads(response)
            if isinstance(obj, dict):
                data = obj.get("data") or obj
            elif isinstance(obj, list):
                data = obj[0] if obj else {}
        except Exception:
            data = None

    err_code = ""
    other_desc = ""
    if isinstance(data, dict):
        err_code = data.get("errorCodeDesc") or ""
        other_desc = data.get("otherDesc") or ""

    if scenario == "Maitrox-数据问题-out of SBOM":
        if err_code and other_desc:
            joined = ", ".join(x.strip() for x in str(other_desc).split(",") if x.strip())
            return f"{err_code}\n超BOM物料: {joined}"
        return err_code
    return err_code
