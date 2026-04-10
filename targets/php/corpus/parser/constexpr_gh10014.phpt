<?php

#[Attribute(+[[][2]?->y]->y)]
class y {
}

(new ReflectionClass(y::class))->getAttributes()[0]->newInstance();

?>