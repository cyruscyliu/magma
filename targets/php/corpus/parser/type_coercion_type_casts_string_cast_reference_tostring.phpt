<?php

class MyClass {
    private $field = 'my string';
    public function &__toString(): string {
        return $this->field;
    }
}

echo new MyClass;

?>