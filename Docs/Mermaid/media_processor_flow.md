graph TD
    A[Start Media Processor] --> B[Initialize MongoDB]
    B --> C[Create Kafka Consumer]
    C --> D[Start Consumer]
    D --> E[Wait for Media Task]
    E --> F{Task Received?}
    F -->|Yes| G[Create TelegramClient]
    G --> H[Get Message]
    H --> I[Download Media]
    I --> J{Media Downloaded?}
    J -->|Yes| K[Process Media File]
    K --> L[Update MongoDB]
    J -->|No| M[Log Error]
    L --> N[Disconnect Client]
    M --> N
    N --> E
    F -->|No| O{Stop Requested?}
    O -->|No| E
    O -->|Yes| P[Stop Consumer]
    P --> Q[End]