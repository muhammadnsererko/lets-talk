# Centralize path configurations
BACKUP_PATHS = {
    'codes': Path(__file__).parent / 'secure_storage/backup_codes.enc',
    'key_rotation_log': Path(__file__).parent / 'logs/rotation.log'
}

BACKUP_PATHS = {
    'codes': Path(__file__).parent / 'secure_storage/backup_codes.enc',
    'recovery': Path(__file__).parent / 'secure_storage/recovery_vault'
}


def validate_paths():
    for key, path in BACKUP_PATHS.items():
        if not path.parent.exists():
            os.makedirs(path.parent, mode=0o700)