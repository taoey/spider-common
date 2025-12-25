-- ----------------------------
-- Table structure for domain
-- ----------------------------
DROP TABLE IF EXISTS "domain";
CREATE TABLE "domain" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "url" TEXT NOT NULL,
  "max_deep" INTEGER,
  "sub_link_extract" TEXT,
  "image_link_extract" TEXT,
  "create_time" INTEGER,
  "update_time" INTEGER
);

-- ----------------------------
-- Table structure for image
-- ----------------------------
DROP TABLE IF EXISTS "image";
CREATE TABLE image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    local_path TEXT,
    alt_text TEXT,
    create_time INTEGER,
    update_time INTEGER
);

-- ----------------------------
-- Table structure for page
-- ----------------------------
DROP TABLE IF EXISTS "page";
CREATE TABLE "page" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "domain_id" INTEGER,
  "parent_id" INTEGER,
  "url" TEXT NOT NULL,
  "title" TEXT,
  "data" TEXT,
  "deep" INTEGER,
  "status" INTEGER,
  "create_time" INTEGER,
  "update_time" INTEGER
);
