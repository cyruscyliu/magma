<?php

class Foo {
    public function method(array $data) {}
}
class Bar extends Foo {
    public function method(array $data): Foo|parent {}
}

?>
DONE