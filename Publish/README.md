# 礼记 - 发布流程

## 流程图 Flowchart

[发布流程图](https://github.com/Lessica/Courtesy-Django/blob/master/Publish/%E3%80%8C%E7%A4%BC%E8%AE%B0%E3%80%8D%E5%8D%A1%E7%89%87%E5%8F%91%E5%B8%83%E6%B5%81%E7%A8%8B.png "发布流程")

## 同步目录结构 Rsync Directory Structure
```
.
└── 8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3
    ├── Content.json
    ├── kCourtesyAttachmentPrefix-9ab7bdc7f0daca92bbaf530e1b4715809e1176607e1ac35922d53c477e8c2f88.png
    ├── kCourtesyAttachmentPrefix-cf9b57d2a9407b991f8f6badeceb995a66bbac2681200f5a4e9b67c1e83c9fde.caf
    ├── kCourtesyAttachmentPrefix-e37b29a585139b118238c054e5f151ffad47d8d8ef9c3d8bb7f7aa74f5cbae7d.png
    ├── kCourtesyAttachmentPrefix-ea0872cc549ac1d673b37abd18ca9f1a3ba1e7bdb4eae943ebc1d200f9c2e635.mov
    ├── kCourtesyThumbnailPrefix-9ab7bdc7f0daca92bbaf530e1b4715809e1176607e1ac35922d53c477e8c2f88-160-160.jpg
    ├── kCourtesyThumbnailPrefix-e37b29a585139b118238c054e5f151ffad47d8d8ef9c3d8bb7f7aa74f5cbae7d-160-160.jpg
    └── kCourtesyThumbnailPrefix-ea0872cc549ac1d673b37abd18ca9f1a3ba1e7bdb4eae943ebc1d200f9c2e635-0-0.jpg

1 directory, 7 files
```

## 同步文件校验 Contents Verification
./Content.json:
```json
{
    "action":"rsync_statics",
    "statics":[
        {
            "filename":"kCourtesyAttachmentPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86.png",
            "type":0,
            "mime":"image/png",
            "sha256":"6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86"
        },
        {
            "filename":"kCourtesyThumbnailPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86-80-80.jpg",
            "type":8,
            "mime":"image/jpeg",
            "sha256":"73a0bbe6183c54200e50824c55eb941c857b658d35c8898b7598d14c3a834489"
        },
        {
            "filename":"kCourtesyThumbnailPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86-160-160.jpg",
            "type":8,
            "mime":"image/jpeg",
            "sha256":"b66928d659746e4034976273ced35065e5d16bfd42be4dea34198e74bd89da77"
        },
        {
            "filename":"kCourtesyThumbnailPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86-320-320.jpg",
            "type":8,
            "mime":"image/jpeg",
            "sha256":"635dd119b1bfb5872accdcbd977767b02d7b4fbcb67900e0e84080f7d80ffaab"
        },
        {
            "filename":"kCourtesyThumbnailPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86-640-640.jpg",
            "type":8,
            "mime":"image/jpeg",
            "sha256":"16f8a5a2773e8c76858df8f188f5327360fee72e42adebd94aac9760ea7fc1e4"
        },
        {
            "filename":"kCourtesyThumbnailPrefix-6f0968011e685553ca61a5f63c9bb39eeaa1e3058f9bd2cb78a3643d01973a86-1280-1280.jpg",
            "type":8,
            "mime":"image/jpeg",
            "sha256":"d40c8ee8da5e0148771d391d0c5c860f5f248acd317da798f405417052e8f93c"
        }
    ],
    "synced_at":1461245945,
    "card_token":"EC47D111-543A-4059-8830-1C5F00087B90",
    "version":16
}
```

## 卡片 Card

- qr_id 二维码标识符 (FK)
- is_editable 是否可修改
- is_public 是否在「探索」版块公开
- view_count 阅读次数
- created_at 创建时间
- modified_at 修改时间
- first_read_at 第一次阅读时间
- visible_at 可见时间
- token 标识符
- edited_count 修改次数
- stars 被收藏次数
- author 作者 (FK)
- read_by 首次阅读者 (FK)
- local_template 卡片数据 (card_data)
- newcard 是否为新发布的卡片

## 卡片数据 Card Data

- shouldAutoPlayAudio 是否自动播放音频 (YES or NO)
- fontType 字体类型
```c
typedef enum : NSUInteger {
    kCourtesyFontDefault = 0,
    kCourtesyFontFZSSK   = 1,
    kCourtesyFontFZHTK   = 2,
    kCourtesyFontFZKTK   = 3,
    kCourtesyFontXXMTK   = 4
} CourtesyFontType;
```
- content 卡片内容: 长度不得超过 2000 字符
- fontSize 卡片字体大小: 整型，14 - 22 pt.
- styleID 卡片风格
```c
typedef enum : NSUInteger {
    kCourtesyCardStyleDefault = 0
} CourtesyCardStyleID;
```
- alignmentType 卡片文字对齐方式
```c
typedef NS_ENUM(NSInteger, NSTextAlignment) {
    NSTextAlignmentLeft      = 0,    // Visually left aligned
    NSTextAlignmentCenter    = 1,    // Visually centered
    NSTextAlignmentRight     = 2,    // Visually right aligned
    NSTextAlignmentJustified = 3,    // Fully-justified. The last line in a paragraph is natural-aligned.
    NSTextAlignmentNatural   = 4,    // Indicates the default alignment for script
} NS_ENUM_AVAILABLE_IOS(6_0);
```
- attachments_hashes 卡片附件标识符数组
- card_token 卡片标识符
- attachments 卡片附件数组

## 卡片附件数据 Card Attachments Data

- type 卡片类型
```c
typedef NS_ENUM(NSInteger, CourtesyAttachmentType) {
    CourtesyAttachmentImage = 0,
    CourtesyAttachmentAudio = 1,
    CourtesyAttachmentVideo = 2,
//    CourtesyAttachmentDraw  = 3,
    CourtesyAttachmentAnimatedImage = 4,
//    CourtesyAttachmentLivePhoto     = 5,
    CourtesyAttachmentThumbnailImage = 8
};
```
- title 卡片描述: 长度不得超过 24 个字符
- attachment_id 服务器给定附件标识符 (弃用 deprecated)
- salt_hash 带盐的附件 sha256 校验值
- location 附件元素在卡片内容中应该占据的起始位置
- length 附件元素在卡片内容中应该占据的结束位置: location + length 不得超过卡片内容长度索引
- thumbnails 附件的缩略图数组

## 缩略图等附加资源数据 Extra Resource Data

- filename 资源文件名
- sha256 资源 sha256 校验值
- mime 资源 MIME 头
- type 资源类型 (与附件类型相同)

## 卡片示例 Sample of Card (local_template)
```json
{
    "is_public":true,
    "author":{
        "registered_at":1459181174,
        "last_login_at":1461250719,
        "card_count":0,
        "user_id":4,
        "email":"i.82@qq.com",
        "profile":{
            "avatar":"b10eec2cdaf08abd437a70dbfe82d221",
            "nick":"i_82",
            "city":"扬州市",
            "mobile":"13270593207",
            "gender":0,
            "area":"邗江区",
            "birthday":"1996-06-18",
            "introduction":"Love is a play that a person who gets gains and losses!",
            "province":"江苏省"
        }
    },
    "is_editable":false,
    "visible_at":0,
    "created_at":1461251328,
    "view_count":0,
    "read_by":"",
    "local_template":{
        "shouldAutoPlayAudio":false,
        "fontType":0,
        "content":"说点什么吧…… ￼ ",
        "fontSize":16,
        "styleID":0,
        "alignmentType":0,
        "attachments":[
            {
                "length":19,
                "thumbnails":[
                    {
                        "filename":"kCourtesyThumbnailPrefix-429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a-80-80.jpg",
                        "type":8,
                        "mime":"image/jpeg",
                        "sha256":"f7ad8f0b2bea39c2917c10ed66fa3dcff16d048512b846f765053d2f58981d6d"
                    },
                    {
                        "filename":"kCourtesyThumbnailPrefix-429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a-160-160.jpg",
                        "type":8,
                        "mime":"image/jpeg",
                        "sha256":"c170bd0ca16ca1e7448065ffa3baa52f749a78d74f026b990cd4f295a71a2e46"
                    },
                    {
                        "filename":"kCourtesyThumbnailPrefix-429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a-320-320.jpg",
                        "type":8,
                        "mime":"image/jpeg",
                        "sha256":"e4298f7ba385bb60f150ab1579dd53f471359b5e46efaa07c21039fef6aeee2b"
                    },
                    {
                        "filename":"kCourtesyThumbnailPrefix-429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a-640-640.jpg",
                        "type":8,
                        "mime":"image/jpeg",
                        "sha256":"753a4cc8c4d43d458c67f014f205701b3347f1bdc019b34729cf1012d645a00d"
                    },
                    {
                        "filename":"kCourtesyThumbnailPrefix-429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a-1280-1280.jpg",
                        "type":8,
                        "mime":"image/jpeg",
                        "sha256":"108b095a0f1461f9bbd41afea3b80785f12adafbca5345f31a9657d1217eae94"
                    }
                ],
                "uploaded_at":1461251328,
                "location":8,
                "salt_hash":"429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a",
                "title":"",
                "type":0,
                "card_token":"250FB606-2869-4FCB-9B5D-8BF77E6ACA96"
            }
        ],
        "attachments_hashes":[
            "429a723e8d55677d5cd62008d5bff0ac2f31d50e780ab307a09993995db93b4a"
        ],
        "card_token":"250FB606-2869-4FCB-9B5D-8BF77E6ACA96"
    },
    "token":"250FB606-2869-4FCB-9B5D-8BF77E6ACA96",
    "stars":0,
    "edited_count":0,
    "modified_at":1461251328,
    "first_read_at":null
}
```
