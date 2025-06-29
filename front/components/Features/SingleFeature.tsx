import { Feature } from "@/types/feature";

interface SingleFeatureProps {
  feature: Feature;
}

const SingleFeature = ({ feature }: SingleFeatureProps) => {
  const { icon, title, bullets } = feature;
  return (
    <div className="w-full">
      <div className="wow fadeInUp" data-wow-delay=".15s">
        <div className="mb-10 flex h-[70px] w-[70px] items-center justify-center rounded-md bg-primary bg-opacity-10 text-primary text-2xl">
          {icon}
        </div>
        <h3 className="mb-5 text-xl font-bold text-black dark:text-white sm:text-2xl lg:text-xl xl:text-2xl">
          {title}
        </h3>
        <ul className="list-disc list-inside text-base font-medium leading-relaxed text-body-color">
          {bullets.map((bullet, index) => (
            <li key={index}>{bullet}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SingleFeature;
