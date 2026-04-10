<?php

interface I {
    public mixed $i { get; }
}

class C extends P implements I {}

class P {
    #[\Override]
    public mixed $i;
}

echo "Done";

?>