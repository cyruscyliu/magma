<?php
class MyException extends Exception
{
    private bool $modified = false;

    protected $code {
        set($value) {
            if ($this->modified) {
                throw new Exception();
            } else {
                $this->modified = true;

                $this->code = $value;
            }
        }
    }
}

$e = new MyException("foo", 1, new Exception());

try {
    $e->__construct("bar", 2, null);
} catch (Exception) {
}

var_dump($e->getMessage());
var_dump($e->getCode());
var_dump($e->getPrevious()::class);

?>