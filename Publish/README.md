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
