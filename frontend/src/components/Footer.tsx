import { Link } from "react-router-dom";

const links = [
    {
        title: 'Features',
        href: '#features',
    },
    {
        title: 'Predict',
        href: '#predict',
    },
    {
        title: 'Research',
        href: '#research',
    },
    {
        title: 'About',
        href: '#about',
    },
    {
        title: 'Help',
        href: '#help',
    },
    {
        title: 'Contact',
        href: '#contact',
    },
];

export default function Footer() {
    return (
        <footer className="bg-black border-t border-gray-800 py-12">
            <div className="mx-auto max-w-5xl px-6">
                <div className="flex flex-wrap justify-between gap-12">
                    <div className="order-last flex items-center gap-3 md:order-first">
                        <span className="text-gray-400 text-sm">© {new Date().getFullYear()} ChemPredict AI, All rights reserved</span>
                    </div>

                    <div className="order-first flex flex-wrap gap-x-6 gap-y-4 md:order-last">
                        {links.map((link, index) => (
                            <a
                                key={index}
                                href={link.href}
                                className="text-gray-400 hover:text-white transition-colors duration-150 text-sm">
                                <span>{link.title}</span>
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </footer>
    );
}
