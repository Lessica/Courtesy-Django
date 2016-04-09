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
    "action": "rsync_statics",
    "version": 16,
    "card_token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3",
    "synced_at": 1460211545,
    "statics": [
        {
            "filename": "kCourtesyAttachmentPrefix-9ab7bdc7f0daca92bbaf530e1b4715809e1176607e1ac35922d53c477e8c2f88.png",
            "sha256": "9ab7bdc7f0daca92bbaf530e1b4715809e1176607e1ac35922d53c477e8c2f88",
            "mime": "image/png",
            "type": 0,
            "thumbnail": false
        },
        {
            "filename": "kCourtesyAttachmentPrefix-cf9b57d2a9407b991f8f6badeceb995a66bbac2681200f5a4e9b67c1e83c9fde.caf",
            "sha256": "cf9b57d2a9407b991f8f6badeceb995a66bbac2681200f5a4e9b67c1e83c9fde",
            "mime": "audio/caf",
            "type": 1,
            "thumbnail": false
        },
        {
            "filename": "kCourtesyAttachmentPrefix-e37b29a585139b118238c054e5f151ffad47d8d8ef9c3d8bb7f7aa74f5cbae7d.png",
            "sha256": "e37b29a585139b118238c054e5f151ffad47d8d8ef9c3d8bb7f7aa74f5cbae7d",
            "mime": "image/png",
            "type": 0,
            "thumbnail": false
        },
        {
            "filename": "kCourtesyAttachmentPrefix-ea0872cc549ac1d673b37abd18ca9f1a3ba1e7bdb4eae943ebc1d200f9c2e635.mov",
            "sha256": "ea0872cc549ac1d673b37abd18ca9f1a3ba1e7bdb4eae943ebc1d200f9c2e635",
            "mime": "video/quicktime",
            "type": 2,
            "thumbnail": false
        },
        {
            "filename": "kCourtesyThumbnailPrefix-9ab7bdc7f0daca92bbaf530e1b4715809e1176607e1ac35922d53c477e8c2f88-160-160.jpg",
            "sha256": "b1b222ad5c64eedda693e605daf32defbf95c6928c48dc1a93dadb2dda58f0fc",
            "mime": "image/jpg",
            "type": 0,
            "thumbnail": true
        },
        {
            "filename": "kCourtesyThumbnailPrefix-e37b29a585139b118238c054e5f151ffad47d8d8ef9c3d8bb7f7aa74f5cbae7d-160-160.jpg",
            "sha256": "f27cf6583a054f85dd0a24a248b5aa64d59d2774ce2573bc26a93f4f26c3e4de",
            "mime": "image/jpg",
            "type": 0,
            "thumbnail": true
        },
        {
            "filename": "kCourtesyThumbnailPrefix-ea0872cc549ac1d673b37abd18ca9f1a3ba1e7bdb4eae943ebc1d200f9c2e635-0-0.jpg",
            "sha256": "300bec40d5baa56dd2de9457b39c1cafea845442cedc18622ec22a9b3c85dc4c",
            "mime": "image/jpg",
            "type": 0,
            "thumbnail": true
        }
    ]
}
```
