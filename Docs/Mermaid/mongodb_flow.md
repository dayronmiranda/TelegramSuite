graph TD
    A[Start] --> B[Initialize MongoDB]
    B --> C[Create AsyncIOMotorClient]
    C --> D[Set Database]
    D --> E[Create File Hash Index]
    A --> F[Close MongoDB]
    F --> G[Close Client Connection]
    A --> H[Get DB Function]
    H --> I[Return DB Instance]
