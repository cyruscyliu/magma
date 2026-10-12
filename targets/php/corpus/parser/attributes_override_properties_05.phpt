<?php

interface I {
    #[\Override]
    public mixed $i { get; }
}

interface II extends I {}


class C implements II {
    public mixed $i;
}

class C2 implements I {
    public mixed $i;
}

echo "Done";

?>