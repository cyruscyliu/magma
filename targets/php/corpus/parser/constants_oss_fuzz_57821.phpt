<?php
class Foo {
    const Foo = 'foo';
}
const C = Foo::{Foo::class};
var_dump(C);
?>