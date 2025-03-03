import { Button, Description, Field, Input, Label } from '@headlessui/react';

export default function JoinClassWidget({ className }) {
  return (
    <form className={className}>
      <img
        src="/public/learnblocks.svg"
        alt="LearnBlocks Logo"
        className="max-h-1/3"
      />
      <Field className='flex flex-col justify-center px-4 g-1'>
        <Label className='font-semibold text-xl '> Class code </Label>
        <Input className='bg-zinc-900 rounded '></Input>
        <hr className='text-zinc-500 mt-1'/>
        <Description className='text-xs text-zinc-400 text-justify'>
          The class instructor should provide this code to join their class
        </Description>
      </Field>
      <Button
        type='submit'
        onClick={(e) => e.preventDefault()}
        className="transition-color rounded-full border-2 border-amber-700 shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800 w-3/6"
      >
        Join
      </Button>
    </form>
  );
}
