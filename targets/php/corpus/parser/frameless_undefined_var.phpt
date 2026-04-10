<?php
set_error_handler(function ($errno, $errstr) {
    throw new Exception($errstr);
});
function test() {
    strpos($foo, 'o');
}
try {
    test();
} catch (Exception $e) {
    echo $e->getMessage(), "\n";
}
?>