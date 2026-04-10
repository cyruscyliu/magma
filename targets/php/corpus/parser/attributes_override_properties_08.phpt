<?php

trait T {
    #[\Override]
    public mixed $i;
}

interface I {
    public mixed $i { get; }
}

class Foo implements I {
    use T;
}

echo "Done";

?>