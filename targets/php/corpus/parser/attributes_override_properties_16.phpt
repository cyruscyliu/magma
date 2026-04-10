<?php

interface I {
    public mixed $i { get; }
}

new class () implements I {
    public mixed $i;

    #[\Override]
    public mixed $c;
};

echo "Done";

?>