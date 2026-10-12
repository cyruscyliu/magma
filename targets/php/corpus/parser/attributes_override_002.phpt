<?php

class Foo implements IteratorAggregate
{
    #[\Override]
    public function getIterator(): Traversable
    {
        yield from [];
    }
}

echo "Done";

?>