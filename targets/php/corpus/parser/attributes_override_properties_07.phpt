<?php

trait T {
    #[\Override]
    public mixed $t;
}

class Foo {
    use T;
}

echo "Done";

?>