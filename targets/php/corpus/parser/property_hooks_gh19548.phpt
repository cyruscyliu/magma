<?php

interface I {
    public mixed $i { get; }
}
class P {
    public mixed $i;
}

class C extends P implements I {}

echo "Test passed - no segmentation fault\n";

?>