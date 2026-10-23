# FetchXML（D365 报错日志查询）

用 `mcp__dataverse_prd__execute_fetchxml`，`entitySetName=new_integrationlogs`。

查询条件：statecode=0，integration scenario in [8 个场景]，statuscode in [100000003(Failed)/100000001(Retry Failed)]，createdon=last-seven-days。按 createdon 降序。

```xml
<fetch version="1.0" output-format="xml-platform" mapping="logical" distinct="true" userqueryid="5c4c9857-6d9f-f111-b8db-000d3ab8437d" no-lock="false">
  <entity name="new_integrationlog">
    <attribute name="statecode"/>
    <attribute name="new_name"/>
    <attribute name="createdon"/>
    <attribute name="new_integrationscenarioid"/>
    <attribute name="statuscode"/>
    <attribute name="new_integrationlogid"/>
    <attribute name="new_requestjson"/>
    <attribute name="new_responsejson"/>
    <attribute name="new_extensionfield1"/>
    <attribute name="new_extensionfield2"/>
    <attribute name="new_extensionfield3"/>
    <attribute name="new_extensionfield4"/>
    <attribute name="new_extensionfield5"/>
    <order attribute="createdon" descending="true"/>
    <filter type="and">
      <filter type="and"><condition attribute="statecode" operator="eq" value="0"/></filter>
      <filter type="and">
        <filter type="and">
          <condition attribute="new_integrationscenarioid" operator="in">
            <value uiname="Push WO to SCM" uitype="new_integrationscenario">{38aed1be-7e62-f111-a825-7c1e52fcf3e4}</value>
            <value uiname="B2X Create WO Request" uitype="new_integrationscenario">{f651f305-e26a-f111-a826-7ced8d484f6b}</value>
            <value uiname="B2X Job Cancel" uitype="new_integrationscenario">{11fe084c-7d62-f111-a825-7c1e52fcf3e4}</value>
            <value uiname="B2X Job Create" uitype="new_integrationscenario">{21c2330b-7d62-f111-a825-7c1e52fcf3e4}</value>
            <value uiname="B2X Update WO Request" uitype="new_integrationscenario">{7324fd48-e26a-f111-a826-7ced8d484f6b}</value>
            <value uiname="MySav Create WO Request" uitype="new_integrationscenario">{ec7cdf10-746b-f111-ab0e-7c1e5237236a}</value>
            <value uiname="MySav Update WO Request" uitype="new_integrationscenario">{0431d823-746b-f111-ab0e-7c1e5237236a}</value>
            <value uiname="Update WO Request" uitype="new_integrationscenario">{5221da59-756b-f111-ab0e-7c1e5237236a}</value>
          </condition>
        </filter>
        <filter type="and">
          <condition attribute="statuscode" operator="in"><value>100000003</value><value>100000001</value></condition>
          <condition attribute="createdon" operator="last-seven-days"/>
        </filter>
      </filter>
    </filter>
    <link-entity name="new_integrationscenario" from="new_integrationscenarioid" to="new_integrationscenarioid" visible="false" link-type="outer" alias="a_208b9d7ba4714804b1c519c506ffca4f">
      <attribute name="new_sourcesystem"/><attribute name="new_targetsystem"/>
    </link-entity>
    <attribute name="new_businessmessage"/>
    <attribute name="new_workorder"/>
    <link-entity name="new_workorder" from="new_workorderid" to="new_workorder" link-type="outer" alias="a_0bbd1e7b159447d880264778ef724bf5" visible="false">
      <attribute name="statuscode"/><attribute name="new_b2xorderid"/><attribute name="new_servicetypecode"/><attribute name="new_workordersourcecode"/>
      <link-entity name="new_servicestore" from="new_servicestoreid" to="new_servicestoreid" link-type="outer" alias="a_servicestore" visible="false">
        <attribute name="new_name"/><attribute name="new_servicestorecode"/>
      </link-entity>
    </link-entity>
  </entity>
</fetch>
```

## 返回 JSON 中提取的关键字段
| D365 字段 | Base 映射 |
|---|---|
| `new_integrationlogid` | 日志ID |
| `new_name` | 工单号（**只写 link-entity workorder 的 FormattedValue，即 WO 开头格式**） |
| `createdon` | Created On（转北京时间 UTC+8） |
| `_new_integrationscenarioid_value` | 场景 GUID（映射见 common.py） |
| `a_208b...new_targetsystem` | Target System |
| `a_208b...new_sourcesystem` | Source System |
| `new_requestjson` | Request JSON |
| `new_responsejson` | Response JSON |
| `a_0bbd...statuscode` | Status Reason / Work Order Status |
| `a_0bbd...new_b2xorderid` | B2X Order ID |
| `a_0bbd...new_servicetypecode` | Service Type |
| `a_0bbd...new_workordersourcecode` | Work Order Source |
| `a_servicestore.new_name` | Service Store Name（新增） |
| `_new_workorder_value` | 工单ID |
