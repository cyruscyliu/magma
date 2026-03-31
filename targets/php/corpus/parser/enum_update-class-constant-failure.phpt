<?php

enum Foo: string {
    const Bar = NONEXISTENT;
}

var_dump(Foo::Bar);

?>