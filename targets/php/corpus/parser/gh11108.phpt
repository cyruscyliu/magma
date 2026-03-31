<?php
register_shutdown_function(function() {
    include __DIR__ . '/gh11108_shutdown.inc';
});
include __DIR__ . '/gh11108_test.inc';
?>