<?php

class C {
    public function __destruct() {
        static $again = true;
        if ($again) {
            $again = false;
            $c = new C;
        }
        throw new Exception;
    }
}

$c = new C;

?>