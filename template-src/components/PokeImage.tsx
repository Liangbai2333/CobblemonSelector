export default function PokeImage({
  name,
  image,
}: {
  name: string;
  image: string;
}) {
  return (
    <img
        className="w-16 h-16 rounded-full"
        src={image}
        alt={name}
      />
  );
}