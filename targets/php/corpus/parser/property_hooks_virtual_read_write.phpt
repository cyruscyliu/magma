<?php

class Test {
    public $prop {
        get => $this->getProp();
        set {
            $this->setProp($value);
        }
    }

    private function getProp() {
        return $this->prop;
    }

    private function setProp($value) {
        $this->prop = $value;
    }
}

$test = new Test;

try {
    $test->prop = 0;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    var_dump($test->prop);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>