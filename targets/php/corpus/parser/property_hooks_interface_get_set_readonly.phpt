<?php
interface I {
    public int $prop { get; set; }
}
class C implements I {
    public function __construct(public readonly int $prop) {}
}
?>