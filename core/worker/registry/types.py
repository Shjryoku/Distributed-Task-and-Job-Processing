import enum

class TaskType(str, enum.Enum):
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    SEND_NOTIFICATION = "send_notification"
    
    PROCESS_IMAGE = "process_image"
    RESIZE_IMAGE = "resize_image"
    GENERATE_THUMBNAIL = "generate_thumbnail"

    GENERATE_REPORT = "generate_report"
    RECALCULATE_STATS = "recalculate_stats"
    AGGREGATE_DATA = "aggregate_data"

    CLEANUP_CACHE = "cleanup_cache"
    DELETE_EXPIRED_DATA = "delete_expired_data"
    SYNC_EXTERNAL_SERVICE = "sync_external_service"

    CREATE_USER_PROFILE = "create_user_profile"
    UPDATE_USER_STATS = "update_user_stats"
    TRACK_EVENT = "track_event"