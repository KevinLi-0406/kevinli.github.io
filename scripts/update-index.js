const fs = require("fs");
const path = require("path");

const rootDir = path.resolve(__dirname, "..");
const indexPath = path.join(rootDir, "index.html");

const START_MARKER = "// PROJECTS_START";
const END_MARKER = "// PROJECTS_END";

function escapeText(value) {
  return String(value || "")
    .replace(/\s+/g, " ")
    .trim();
}

function removeHtmlTags(value) {
  return escapeText(
    String(value || "")
      .replace(/<[^>]*>/g, "")
      .replace(/&nbsp;/gi, " ")
      .replace(/&amp;/gi, "&")
      .replace(/&lt;/gi, "<")
      .replace(/&gt;/gi, ">")
      .replace(/&quot;/gi, '"')
      .replace(/&#39;/gi, "'")
  );
}

function getProjectTitle(filename, html) {
  const h1Match = html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i);

  if (h1Match) {
    const h1Title = removeHtmlTags(h1Match[1]);

    if (h1Title) {
      return h1Title;
    }
  }

  const titleMatch = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);

  if (titleMatch) {
    const pageTitle = removeHtmlTags(titleMatch[1]);

    if (pageTitle) {
      return pageTitle
        .replace(/\s*[|｜-]\s*.*$/, "")
        .trim();
    }
  }

  return filename.replace(/\.html?$/i, "");
}

function getProjectDescription(filename, html) {
  const descriptionMatch = html.match(
    /<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i
  );

  if (descriptionMatch && descriptionMatch[1].trim()) {
    return escapeText(descriptionMatch[1]);
  }

  const title = filename.replace(/\.html?$/i, "");

  return `${title}网页项目，点击查看详细内容。`;
}

function getProjectIcon(filename, title) {
  const text = `${filename} ${title}`.toLowerCase();

  if (
    text.includes("宝可梦") ||
    text.includes("pokemon") ||
    text.includes("图鉴")
  ) {
    return "⚡";
  }

  if (text.includes("工具") || text.includes("tool")) {
    return "🛠️";
  }

  if (
    text.includes("关于") ||
    text.includes("个人") ||
    text.includes("about")
  ) {
    return "👤";
  }

  if (text.includes("博客") || text.includes("blog")) {
    return "📝";
  }

  if (text.includes("链接") || text.includes("link")) {
    return "🔗";
  }

  if (
    text.includes("项目") ||
    text.includes("作品") ||
    text.includes("project")
  ) {
    return "🚀";
  }

  return "📄";
}

function getProjects() {
  const files = fs
    .readdirSync(rootDir, { withFileTypes: true })
    .filter((entry) => {
      return (
        entry.isFile() &&
        /\.html?$/i.test(entry.name) &&
        entry.name.toLowerCase() !== "index.html"
      );
    })
    .map((entry) => entry.name)
    .sort((a, b) => a.localeCompare(b, "zh-CN"));

  return files.map((filename) => {
    const filePath = path.join(rootDir, filename);
    const html = fs.readFileSync(filePath, "utf8");
    const title = getProjectTitle(filename, html);

    return {
      filename,
      title,
      icon: getProjectIcon(filename, title),
      description: getProjectDescription(filename, html)
    };
  });
}

function updateIndex() {
  if (!fs.existsSync(indexPath)) {
    throw new Error(`找不到首页文件：${indexPath}`);
  }

  const indexHtml = fs.readFileSync(indexPath, "utf8");

  const startIndex = indexHtml.indexOf(START_MARKER);
  const endIndex = indexHtml.indexOf(END_MARKER);

  if (startIndex === -1) {
    throw new Error(
      `index.html 中找不到开始标记：${START_MARKER}`
    );
  }

  if (endIndex === -1) {
    throw new Error(
      `index.html 中找不到结束标记：${END_MARKER}`
    );
  }

  if (endIndex <= startIndex) {
    throw new Error("index.html 中的项目标记顺序错误");
  }

  const projects = getProjects();

  const projectCode = [
    START_MARKER,
    `const PROJECTS = ${JSON.stringify(projects, null, 2)};`,
    END_MARKER
  ].join("\n");

  const contentBefore = indexHtml.slice(0, startIndex);
  const contentAfter = indexHtml.slice(
    endIndex + END_MARKER.length
  );

  const updatedHtml =
    contentBefore +
    projectCode +
    contentAfter;

  if (updatedHtml === indexHtml) {
    console.log("项目列表没有变化");
    return;
  }

  fs.writeFileSync(indexPath, updatedHtml, "utf8");

  console.log(`已更新 index.html，共发现 ${projects.length} 个项目：`);

  for (const project of projects) {
    console.log(`- ${project.filename} → ${project.title}`);
  }
}

try {
  updateIndex();
} catch (error) {
  console.error("更新 index.html 失败：");
  console.error(error.message);
  process.exit(1);
}
