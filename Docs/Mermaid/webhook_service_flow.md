graph TD
    A[Start] --> B[Send Webhook Notification]
    B --> C[Create aiohttp Session]
    C --> D[Send POST Request]
    D --> E{Response OK?}
    E -->|Yes| F[End]
    E -->|No| G[Log Error]
    G --> F
