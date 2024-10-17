graph TD
    A[Start] --> B[Define API Router]
    B --> C[Get Task Status Endpoint]
    C --> D[Query Task from DB]
    D --> E[Return Task Status]
    B --> F[Set Webhook Endpoint]
    F --> G[Update Task with Webhook URL]
    G --> H[Return Success]
