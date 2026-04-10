<?php

trait T {
    public abstract $prop { get; set; }
}

class C {
    use T;
}

?>