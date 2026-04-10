<?php

class MyException extends Exception {
    private $field = 'my string';
    public function &__toString(): string {
        return $this->field;
    }
}

// Must not be caught to trigger the issue!
throw new MyException;

?>