<?php
abstract class P {
    protected abstract int $prop { get; set; }
}
class C extends P {
    public function __construct(protected readonly int $prop) {}
}
?>