<?php
$file = __DIR__ . '/gh12366.inc';
// Update timestamp and use opcache.file_update_protection=1 to prevent included file from being persisted in shm.
touch($file);
require $file;
?>