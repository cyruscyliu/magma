<?php

namespace Foo;

class Foo {
    public function &__call($method, $args) {}
}

call_user_func((new Foo)->bar(...));

?>