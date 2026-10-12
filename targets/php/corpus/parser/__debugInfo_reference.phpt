<?php

class Test {
    private $tmp = ['x' => 1];

    public function &__debugInfo(): array
    {
        return $this->tmp;
    }
}

var_dump(new Test);

?>