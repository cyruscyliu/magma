<?php

class ObjectOne
{
    function getNone()
    {
        throw new Exception('NONE');
    }
}

class Proxy
{
    function three($a, $b, $c)
    {
    }

    function callOne()
    {
        try
        {
            $res = new ObjectOne();
            $this->three($res->getNone());
        }
        catch(Exception $e)
        {
            echo 'Caught: '.$e->getMessage()."\n";
        }
    }

    function callTwo()
    {
        try
        {
            $res = new ObjectOne();
            $this->three(1, $res->getNone());
        }
        catch(Exception $e)
        {
            echo 'Caught: '.$e->getMessage()."\n";
        }
    }

    function callThree()
    {
        try
        {
            $res = new ObjectOne();
            $this->three(1, 2, $res->getNone());
        }
        catch(Exception $e)
        {
            echo 'Caught: '.$e->getMessage()."\n";
        }
    }
}

$p = new Proxy();

$p->callOne();
$p->callTwo();
$p->callThree();
?>