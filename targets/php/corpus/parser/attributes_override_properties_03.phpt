<?php

interface I {
    public mixed $i { get; }
}

class P {
    #[\Override]
    public mixed $i;
}

class C extends P implements I {}

echo "Done";

?>