<?php

class P {
    protected function common() {}
}

class A extends P {}

trait T {
    private abstract function common(int $param);
}

class B extends P {
    use T;
}

?>