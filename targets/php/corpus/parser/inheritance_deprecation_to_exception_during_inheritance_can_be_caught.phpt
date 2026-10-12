<?php

set_error_handler(function($code, $message) {
    throw new Exception($message);
});

try {
    class C extends DateTime {
        public function getTimezone() {}
        public function getTimestamp() {}
    };
} catch (Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

var_dump(new C());

?>