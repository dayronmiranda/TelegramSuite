graph TD
    A[Start] --> B[Setup Logging Function]
    B --> C[Create Log Formatter]
    C --> D[Create RotatingFileHandler]
    D --> E[Set Formatter for Handler]
    E --> F[Get Logger]
    F --> G[Set Logger Level]
    G --> H[Add Handler to Logger]
    H --> I[Return Logger]