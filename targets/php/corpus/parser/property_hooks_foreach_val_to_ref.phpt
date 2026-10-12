<?php

class ByVal {
    public $byRef {
        &get {
            $x = 42;
            return $x;
        }
    }
    public $byVal = 'byValue' {
        get => $this->byVal;
        set => $value;
    }
}

function test($object) {
    foreach ($object as $prop => &$value) {
        var_dump($value);
    }
}

try {
    test(new ByVal);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>