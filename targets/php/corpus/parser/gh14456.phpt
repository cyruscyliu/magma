<?php

class PrivateUser {
    private function __construct() {}
    public function __destruct() {
        echo 'Destructor for ', __CLASS__, PHP_EOL;
    }
}

try {
    new PrivateUser();
} catch (Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
?>