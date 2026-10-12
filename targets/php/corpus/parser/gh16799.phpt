<?php
set_error_handler(function($_, $m) { throw new Exception($m); });
class Test {
    static function test() {
        call_user_func("static::ok");
    }
    static function ok() {
    }
}
Test::test();
?>