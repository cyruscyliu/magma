<?php

enum Foo: string {
    case Bar = __FILE__;
}

echo Foo::Bar->value, "\n";

?>