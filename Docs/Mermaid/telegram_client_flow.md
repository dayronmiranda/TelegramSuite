graph TD
    A[Start] --> B[Create Session Function]
    B --> C[Create TelegramClient]
    C --> D[Connect Client]
    D --> E[Return Client]
    A --> F[Close Session Function]
    F --> G[Disconnect Client]
