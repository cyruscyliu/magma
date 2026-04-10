<?php
class Foo {}
class Bar {
    public function __destruct() {
        throw new Exception();
    }
}
in_array(new Foo(), [new Bar()], true);
?>