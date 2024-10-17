graph TD
    A[Start] --> B[Initialize Scheduler]
    B --> C[Start Scheduler]
    A --> D[Schedule Extraction Function]
    D --> E[Add Job to Scheduler]
    E --> F[Return Job ID]
    A --> G[Remove Scheduled Extraction]
    G --> H[Remove Job from Scheduler]
