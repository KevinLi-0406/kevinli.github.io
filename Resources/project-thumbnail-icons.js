/* Fixed thumbnail icons for portal project cards. */
(function () {
  var PROJECT_ICONS = {
    "CherryStudio CSS 编辑器.html": "🎨",
    "golden-puppy-pet.html": "🐥",
    "squirtle-pet.html": "🐢",
    "宝可梦图鉴.html": "📕",
    "奇怪的小鸡毛.html": "🐥",
    "奇怪的杰尼龟.html": "🐢"
  };

  window.getProjectThumbnailIcon = function (fileName) {
    return PROJECT_ICONS[fileName] || "📄";
  };
})();
