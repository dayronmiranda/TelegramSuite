graph TD
    A[Start Extraction] --> B[Create TelegramClient]
    B --> C[Start Client]
    C --> D[Iterate Messages]
    D --> E{Has Message?}
    E -->|Yes| F[Create Message Data]
    F --> G[Send to Kafka Message Topic]
    G --> H{Has Media?}
    H -->|Yes| I[Create Media Task]
    I --> J[Send to Kafka Media Topic]
    H -->|No| D
    E -->|No| K[Update Task Status]
    K --> L{Has Webhook?}
    L -->|Yes| M[Send Webhook Notification]
    L -->|No| N[Disconnect Client]
    M --> N
    N --> O[End]