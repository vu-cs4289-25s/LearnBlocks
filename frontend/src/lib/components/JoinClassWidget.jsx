import { Button, Description, Field, Input, Label } from '@headlessui/react';
import { useContext, useRef } from "react";
import { AuthUserContext, ErrorContext } from "$lib/contexts/ErrorContext";
import { tryJoinClass} from "$lib/utils/actions.mjs";

export default function JoinClassWidget({ className }) {
  const formRef=useRef(null);
  const {authUser}=useContext(AuthUserContext);
  //console.log("authuser",authUser);
  const {setError}=useContext(ErrorContext);
  const onJoin= async(e)=>{
    e.preventDefault();
    const rawFormData = new FormData(formRef.current);
    const data = Object.fromEntries(rawFormData.entries());
    const res= await tryJoinClass(data.classcode,authUser);
    if (res instanceof Error) return setError(res.message);
  }
  return (
    <form className={`${className} p-9 gap-9 rounded-2xl`} ref={formRef}>
      <img
        src="/public/learnblocks.svg"
        alt="LearnBlocks Logo"
        className="max-h-1/3"
      />
      <Field className='flex flex-col justify-center px-4 g-1 gap-2'>
        <Label className='font-semibold text-xl '> Class code: </Label>
        <Input name='classcode' className='bg-zinc-900 rounded '></Input>
        <hr className='text-zinc-500 mt-1'/>
        <Description className='text-xs text-zinc-400 text-justify'>
          The class instructor should provide this code to join their class
        </Description>
      </Field>
      <Button
        type='submit'
        onClick={onJoin}
        className="transition-color rounded-full border-2 border-amber-700 shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800 w-3/6"
      >
        Join
      </Button>
    </form>
  );
}
